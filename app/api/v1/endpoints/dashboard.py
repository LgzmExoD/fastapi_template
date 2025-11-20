from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api import deps
from app.api.v1.endpoints.analytics import (get_system_metrics,
                                            get_tenant_metrics,
                                            get_user_metrics)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
) -> str:
    system = await get_system_metrics(db, current_user)
    users = await get_user_metrics(db, current_user)
    tenants = await get_tenant_metrics(db, current_user)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Dashboard</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root {{
                --bg: #f8f9fa;
                --card-bg: #ffffff;
                --text: #2d3748;
                --text-light: #718096;
                --primary: #3182ce;
                --border: #e2e8f0;
            }}

            body {{
                font-family: -apple-system, sans-serif;
                background: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 40px;
                line-height: 1.5;
            }}

            .layout {{
                max-width: 1200px;
                margin: 0 auto;
            }}

            header {{
                margin-bottom: 40px;
                border-bottom: 1px solid var(--border);
                padding-bottom: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            h1 {{ font-size: 24px; margin: 0; }}

            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 24px;
            }}

            .card {{
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 8px;
                padding: 24px;
            }}

            .card h2 {{
                font-size: 16px;
                color: var(--text-light);
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin: 0 0 20px 0;
            }}

            .stat-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 12px;
                padding-bottom: 12px;
                border-bottom: 1px solid var(--border);
            }}

            .stat-row:last-child {{
                border: none;
                margin: 0;
                padding: 0;
            }}

            .big-number {{
                font-size: 32px;
                font-weight: 700;
                color: var(--primary);
                margin-bottom: 20px;
            }}

            .label {{ color: var(--text-light); font-size: 14px; }}
            .value {{ font-weight: 600; }}

            .refresh {{
                background: white;
                border: 1px solid var(--border);
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                color: var(--text);
            }}
            .refresh:hover {{ background: #f7fafc; }}
        </style>
    </head>
    <body>
        <div class="layout">
            <header>
                <h1>System Overview</h1>
                <button onclick="location.reload()" class="refresh">Refresh</button>
            </header>

            <div class="grid">
                <div class="card">
                    <h2>Users</h2>
                    <div class="big-number">{system['total_users']}</div>
                    <div class="stat-row">
                        <span class="label">Active</span>
                        <span class="value">{system['active_users']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="label">Superadmins</span>
                        <span class="value">{users['superadmins']}</span>
                    </div>
                </div>

                <div class="card">
                    <h2>Tenants</h2>
                    <div class="big-number">{system['total_tenants']}</div>
                    <div class="stat-row">
                        <span class="label">Active</span>
                        <span class="value">{system['active_tenants']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="label">Avg Users/Tenant</span>
                        <span class="value">{users['average_users_per_tenant']}</span>
                    </div>
                </div>

                <div class="card">
                    <h2>Distribution</h2>
                    <div class="stat-row">
                        <span class="label">Tenants w/ Users</span>
                        <span class="value">{tenants['tenants_with_users']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="label">Empty Tenants</span>
                        <span class="value">{tenants['tenants_without_users']}</span>
                    </div>
                    <div class="stat-row">
                        <span class="label">Max Users in Tenant</span>
                        <span class="value">{tenants['max_users_per_tenant']}</span>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

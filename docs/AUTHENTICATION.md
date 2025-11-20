# Authentication

The application uses OAuth2 with Password Flow and JWT tokens.

## Components

- **JWT**: JSON Web Tokens are used for stateless authentication.
- **Access Token**: Short-lived token (default 30 mins) used to access protected resources.
- **Refresh Token**: Long-lived token (default 7 days) used to obtain new access tokens.
- **Password Hashing**: Passwords are hashed using Bcrypt (via Passlib).

## Flow

1.  **Login**: User sends email/password to `/login/access-token`.
2.  **Validation**: Server verifies credentials.
3.  **Token Issue**: Server returns Access Token and Refresh Token.
4.  **Access**: Client sends Access Token in `Authorization: Bearer <token>` header.
5.  **Refresh**: When Access Token expires, Client uses Refresh Token to get a new pair.

## Security

- **Secret Key**: Used to sign JWTs. Must be kept secret.
- **Algorithm**: HS256 is used by default.
- **Scopes**: (Optional) Can be added for fine-grained permissions.

## Implementation Details

- `app/core/security.py`: Helper functions for hashing and token generation.
- `app/api/deps.py`: Dependencies for validating tokens and retrieving the current user.

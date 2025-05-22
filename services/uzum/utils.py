import functools

class TokenExpiredError(Exception):
    """Exception raised when the token is expired."""
    pass



def handle_token_expiration(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):   
        try:
            return await func(self, *args, **kwargs)
        except TokenExpiredError:
            await self.refresh_token()
            return await func(self, *args, **kwargs)
    return wrapper
from custom_libs.fastapi_cache import FastAPICache


def cache_key_builder_with_user_id(*args, **kwargs):
    inner_kwargs = kwargs.get('kwargs', {})
    user = inner_kwargs.get('user', None)
    user_id = str(user.id) if user else 'anonymous'
    return f"cache_key_prefix:{user_id}"


async def clear_user_chache(user):
    user_id = str(user.id)
    cache_key = f"cache_key_prefix:{user_id}"
    return await FastAPICache.clear(key=cache_key)

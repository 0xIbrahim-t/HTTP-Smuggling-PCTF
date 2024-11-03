-- /apache/cache_control.lua
-- Custom cache control implementation

function check_cache_access(r)
    -- Check for admin token
    local auth_header = r.headers_in['Authorization'] or ''
    local is_admin = string.match(auth_header, "Bearer.*role.*admin.*") ~= nil
    
    -- Check for special cache key
    local special_key = r.headers_in['X-Special-Key'] or ''
    local enable_cache = special_key == "secret_cache_key"
    
    -- Set cache control based on conditions
    if is_admin and enable_cache then
        -- Show cached content to admin and then delete
        r:setenv("SHOW_CACHE", "1")
        -- Mark cache for deletion after response
        r:setenv("DELETE_CACHE", "1")
        return apache2.DECLINED
    elseif enable_cache then
        -- Normal caching behavior
        return apache2.DECLINED
    else
        -- Disable caching
        return apache2.OK
    end
end
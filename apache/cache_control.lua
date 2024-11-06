-- /apache/cache_control.lua
-- Vulnerable cache control implementation with admin cache deletion

function check_cache_access(r)
    -- Check for admin token
    local auth_header = r.headers_in['Authorization'] or ''
    local is_admin = string.match(auth_header, "Bearer.*role.*admin.*") ~= nil
    
    -- Check for special cache key
    local special_key = r.headers_in['X-Special-Key'] or ''
    local enable_cache = special_key == "secret_cache_key"
    
    -- Cache control logic
    if is_admin and enable_cache then
        -- Show cached content to admin and mark for deletion
        r:setenv("SHOW_CACHE", "1")
        r:setenv("DELETE_CACHE", "1")  -- Mark for deletion after admin views
        return apache2.DECLINED
    elseif enable_cache then
        -- Allow caching for non-admin requests
        r:setenv("ENABLE_CACHE", "1")
        return apache2.DECLINED
    end
    
    return apache2.OK
end
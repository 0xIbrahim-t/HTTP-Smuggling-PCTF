-- File: apache/cache_control.lua

-- Check if file exists
function file_exists(path)
    local f = io.open(path, "rb")
    if f then 
        f:close()
        return true
    end
    return false
end

function check_and_manage_cache(r)
    -- Get headers
    local auth_header = r.headers_in['Authorization']
    local x_admin = r.headers_in['X-Admin-Request']
    
    -- Check special headers for cache poisoning
    if r.headers_in['X-Special-Key'] == 'special-cache-key-123' and 
       r.headers_in['X-Cache-Control'] == 'need-cache' then
        r.notes["cache_enabled"] = "1"
    end
    
    -- Check if admin request
    local is_admin = false
    if auth_header and auth_header:match("Bearer.*role.*admin") then
        is_admin = true
        r.notes["is_admin"] = "1"
    end
    
    -- Generate cache path
    local uri = r.uri
    local cache_key = uri
    
    -- Hash the cache key
    local hash = ""
    for i = 1, #cache_key do
        hash = hash .. string.format("%02x", string.byte(cache_key:sub(i,i)))
    end
    local cache_path = "/var/cache/apache2/cache_" .. hash
    
    -- Store cache path
    r.notes["cache_path"] = cache_path
    
    -- Log request
    r:info("[Cache] Request: " .. r.method .. " " .. uri)
    r:info("[Cache] Cache path: " .. cache_path)
    
    -- Check for cached content
    if file_exists(cache_path) then
        r:info("[Cache] Cache exists")
        
        -- Set cache hit header
        if r.headers_out then
            r.headers_out['X-Cache-Hit'] = 'true'
        end
        
        -- If admin, mark for deletion
        if is_admin then
            r:info("[Cache] Admin access - will delete")
            r.notes["delete_after_serve"] = "1"
            
            if r.headers_out then
                r.headers_out['X-Cache-Admin-View'] = 'true'
            end
        end
    end
    
    return apache2.OK
end

function handle_response(r)
    -- Check if we need to delete cache
    if r.notes["delete_after_serve"] == "1" then
        local cache_path = r.notes["cache_path"]
        if cache_path and cache_path ~= "" then
            -- Delete cache file
            os.remove(cache_path)
            r:info("[Cache] Deleted: " .. cache_path)
            
            if r.headers_out then
                r.headers_out['X-Cache-Deleted'] = 'true'
            end
        end
    end
    
    return apache2.OK
end
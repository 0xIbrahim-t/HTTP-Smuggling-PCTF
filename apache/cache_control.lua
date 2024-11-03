-- /etc/apache2/lua/cache_control.lua

-- Function to check if a request has potential smuggling headers
function has_smuggling_headers(r)
    local cl = r.headers_in['Content-Length']
    local te = r.headers_in['Transfer-Encoding']
    return cl and te
end

-- Function to extract token from Authorization header
function extract_admin_token(auth_header)
    if auth_header and auth_header:match("Bearer%s+(.+)") then
        return auth_header:match("Bearer%s+(.+)")
    end
    return nil
end

function check_and_manage_cache(r)
    -- Get environment variables and headers
    local auth_header = r.headers_in['Authorization']
    local x_admin_request = r.headers_in['X-Admin-Request']
    local cache_enabled = r:getenv("CACHE_ENABLED")
    local cache_control_valid = r:getenv("CACHE_CONTROL_VALID")
    
    -- Check if request is from admin bot
    local is_admin = false
    if auth_header and x_admin_request == 'true' then
        local token = extract_admin_token(auth_header)
        if token then
            is_admin = true
            r:setenv("IS_ADMIN", "1")
        end
    end
    
    -- Function to check if file exists
    local function file_exists(path)
        local file = io.open(path, "rb")
        if file then file:close() return true end
        return false
    end
    
    -- Generate cache path based on URI and query string
    local uri = r:uri()
    local args = r:args()
    local cache_key = uri
    if args and args ~= "" then
        cache_key = cache_key .. "?" .. args
    end
    
    -- Hash the cache key to create filename
    local hash = ""
    for i = 1, #cache_key do
        hash = hash .. string.format("%02x", string.byte(cache_key, i))
    end
    local cache_path = string.format("/var/cache/apache2/cache_%s", hash)
    
    -- Store cache path for later use
    r:setenv("CACHE_PATH", cache_path)
    
    -- Log request details
    r:info(string.format("[Cache] Request: %s %s", r:method(), cache_key))
    r:info(string.format("[Cache] Path: %s", cache_path))
    
    -- Handle caching logic
    if cache_enabled == "1" and cache_control_valid == "1" then
        -- This is a request that wants to set cache
        r:setenv("CACHE_THIS", "1")
        r:info("[Cache] Caching enabled for request")
        
        -- If this is a smuggling attempt, log it
        if has_smuggling_headers(r) then
            r:info("[Cache] Potential HTTP smuggling detected")
        end
        
        return apache2.OK
    end
    
    -- Check for cached content
    if file_exists(cache_path) then
        r:info("[Cache] Cached content exists")
        r:setenv("SERVE_CACHE", "1")
        
        -- Only set delete flag if admin
        if is_admin then
            r:info("[Cache] Admin accessing cached content - will delete after serve")
            r:setenv("DELETE_AFTER_SERVE", "1")
            r:headers_out():set("X-Cache-Admin-View", "true")
            r:headers_out():set("X-Cache-Will-Delete", "true")
        end
        
        -- Add cache hit header for everyone
        r:headers_out():set("X-Cache-Hit", "true")
    end
    
    return apache2.OK
end

-- Function to handle response and cleanup
function handle_response(r)
    if r:getenv("DELETE_AFTER_SERVE") == "1" then
        local cache_path = r:getenv("CACHE_PATH")
        if cache_path then
            -- Delete the cache file only after admin view
            os.remove(cache_path)
            r:info(string.format("[Cache] Admin viewed - deleted cache: %s", cache_path))
            
            -- Add headers to help with exploitation
            r:headers_out():set("X-Cache-Deleted", "true")
            r:headers_out():set("X-Cache-Path", cache_path)
        end
    end
    return apache2.OK
end
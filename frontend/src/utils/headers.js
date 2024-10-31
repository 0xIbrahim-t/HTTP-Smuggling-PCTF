// Vulnerable: Predictable header generation
export const generateFrontendVersion = () => {
    return 'v1';
  };
  
  // Vulnerable: Weak header generation for admin endpoints
  export const generateServiceAuth = (timestamp = Date.now()) => {
    return `${timestamp}-${btoa('admin-service')}`;
  };
  
  // Vulnerable: Reuses CSP nonce
  export const getCurrentNonce = () => {
    return window.__nonce || '';
  };
  
  // Vulnerable: Allows header manipulation
  export const createRequestHeaders = (isAdmin = false) => {
    const headers = {
      'X-Frontend-Version': generateFrontendVersion(),
      'Content-Type': 'application/json'
    };
  
    if (isAdmin) {
      headers['X-Service-Auth'] = generateServiceAuth();
    }
  
    const token = localStorage.getItem('token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
  
    return headers;
  };
  
  export const addCacheHeaders = (headers = {}) => {
    return {
      ...headers,
      'X-Frontend-Version': generateFrontendVersion(),
      'Cache-Control': 'max-age=3600'
    };
  };
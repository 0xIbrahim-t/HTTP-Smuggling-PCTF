export const setAuthToken = (token) => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  };
  
  export const getAuthToken = () => {
    return localStorage.getItem('token');
  };
  
  export const isAdmin = () => {
    const token = getAuthToken();
    if (!token) return false;
    
    try {
      // Decode JWT without verification (vulnerable)
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.role === 'admin';
    } catch {
      return false;
    }
  };
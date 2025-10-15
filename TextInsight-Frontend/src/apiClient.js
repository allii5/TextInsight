import axios from 'axios';

// Create an Axios instance
const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000',
});

// List of endpoints that do not require the access token
const noAuthEndpoints = [
    '/auth/api/login/',
    '/auth/api/signup-teacher/',
    '/auth/api/verify-email/',
    '/auth/api/reset-password/',
    '/auth/api/forgot-password/',
];

// Request interceptor to conditionally add the access token to the headers
apiClient.interceptors.request.use(
    config => {
        const accessToken = localStorage.getItem('access_token');
        const isNoAuthEndpoint = noAuthEndpoints.some(endpoint => config.url.includes(endpoint));

        if (accessToken && !isNoAuthEndpoint) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
    response => {
        return response;
    },
    async error => {
        const originalRequest = error.config;

        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh_token');

            if (refreshToken) {
                try {
                    const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
                        refresh: refreshToken,
                    });

                    const newAccessToken = response.data.access;
                    localStorage.setItem('access_token', newAccessToken);

                    originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                    return apiClient(originalRequest);
                } catch (refreshError) {
                    // Handle refresh token error (e.g., redirect to login)
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/';
                    return Promise.reject(refreshError);
                }
            }
        }

        return Promise.reject(error);
    }
);

export default apiClient;

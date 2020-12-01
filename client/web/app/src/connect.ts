import Axios, { AxiosInstance } from 'axios';

const connect:AxiosInstance = Axios.create({
    timeout: 1000,
    withCredentials: true,
    headers: {
        'content-type': 'application/json'
    },
    xsrfHeaderName: 'X-CSRFToken',
    xsrfCookieName: 'csrftoken',
    baseURL: process.env.VUE_APP_ROOT_API
})

export default connect;
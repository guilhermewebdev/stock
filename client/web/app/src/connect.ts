import Axios, { AxiosInstance } from 'axios';

const connect:AxiosInstance = Axios.create({
    baseURL: 'http://localhost/api/',
    timeout: 1000,
})

export default connect;
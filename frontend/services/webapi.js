import axios from "axios"

export const fetcher = url => axios.get(url).then(res => res.data)

export const BASE_URL = "https://nhl-elo-api-app.herokuapp.com"

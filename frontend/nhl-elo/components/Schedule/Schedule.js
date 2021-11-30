import axios from "axios"
import { useQuery } from "react-query"
import styles from './Schedule.module.css'

export default function Schedule() {
  const eloTableUrl = "https://nhl-elo-api.herokuapp.com/elotable"
  const { isLoading, isError, data, error } = useQuery("fetchEloTable", async () => {
    const { data } = await axios.get(eloTableUrl)
    return data
  })

  return (
    <div className={styles.schedule}>
    </div>
  )
}

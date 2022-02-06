import useSWR from "swr"
import { BASE_URL, fetcher } from "../../services/webapi"
import styles from "./GameCardSection.module.css"

export default function GameCardSection() {
  const { data, error } = useSWR(`${BASE_URL}/eloschedule?window=close`, fetcher)
  const isLoading = !data && !error

  console.log(data)

  return (
    <div className={styles.gameCardSection}>
      <h1>{"today's games"}</h1>
      <div className="accentDiv" />
    </div>
  )
}

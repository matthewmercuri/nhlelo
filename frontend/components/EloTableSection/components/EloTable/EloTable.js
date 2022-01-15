import { useState } from "react"
import useSWR from "swr"
import { BASE_URL, fetcher } from "../../../../services/webapi"
import styles from './EloTable.module.css'

export default function EloTable() {
  const { data, error } = useSWR(`${BASE_URL}/teamelotable`, fetcher)
  const [showAll, setShowAll] = useState(false)
  const isLoading = !data && !error

  console.log(data)
  console.log(isLoading)
  console.log(showAll)

  return (
    <div className={styles.eloTableContainer}>
      <table className={styles.eloTable} cellSpacing={0}>
        <tr>
          <th className={styles.endCol}>position</th>
          <th>team</th>
          <th className={styles.endCol}>elo</th>
        </tr>
        {data && data.data && (
          data.data.map((row, index) => {
            const teamName = Object.keys(row)[0]
            const teamElo = Math.round(row[teamName])
            const teamRank = index + 1
            const eloStyle = teamElo >= 1500 ? styles.eloIndicatorGood : styles.eloIndicatorBad

            if (teamRank > 10 && !showAll) return null

            return (
              <tr key={teamName}>
                <td>{teamRank}</td>
                <td>{teamName}</td>
                <td>
                  <div className={styles.eloIndicatorContainer}>
                    <div className={eloStyle}>{teamElo}</div>
                  </div>
                </td>
              </tr>
            )
          })
        )}
      </table>
      {data && data.data && (
        <div onClick={() => setShowAll(!showAll)} className={styles.showAllButton}>
          {!showAll ? "show all" : "collapse all"}
        </div>
      )}
    </div>
  )
}

import axios from "axios"
import { useQuery } from "react-query"
import TeamRank from "../TeamRank"
import styles from './Rankings.module.css'

export default function Rankings() {
  const eloRankingsUrl = "https://nhl-elo-api.herokuapp.com/teamelos"
  const { isLoading, isError, data, error } = useQuery("fetchTeamElos", async () => {
    const { data } = await axios.get(eloRankingsUrl)
    return data
  })

  return (
    <div className={styles.rankings}>
      {isLoading ? <p>loading...</p> : (
        data.data.map((teamData) => {
          return <TeamRank key={teamData} teamData={teamData} />
        })
      )}
    </div>
  )
}

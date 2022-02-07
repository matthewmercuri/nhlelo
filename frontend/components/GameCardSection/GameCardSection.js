import useSWR from "swr"
import { BASE_URL, fetcher } from "../../services/webapi"
import LoadingSpinner from "../LoadingSpinner"
import GameCard from "./components/GameCard"
import styles from "./GameCardSection.module.css"

export default function GameCardSection() {
  const { data, error } = useSWR(`${BASE_URL}/eloschedule?window=close`, fetcher)
  const isLoading = !data && !error

  return (
    <div className={styles.gameCardSection}>
      <h1>{"today's games"}</h1>
      <div className="accentDiv" />
      <div className={styles.gameCardSectionCards}>
        {isLoading && <LoadingSpinner size={"large"} />}
        {!isLoading && data.data.today.length == 0 && (
          <p className={styles.noGames}>There are no games scheduled for today.</p>
        )}
        {!isLoading && data.data.today.length > 0 && (
          data.data.today.map(gameData => {
            return (
              <GameCard
                key={`${gameData.awayTeam}${gameData.dateEst}`}
                gameData={gameData}
              />
            )
          })
        )}
      </div>
      <h1>{"tomorrow's games"}</h1>
      <div className="accentDiv" />
      <div className={styles.gameCardSectionCards}>
        {!isLoading && data.data.tomorrow.length == 0 && (
          <p className={styles.noGames}>There are no games scheduled for tomorrow.</p>
        )}
        {!isLoading && data.data.tomorrow.length > 0 && (
          data.data.tomorrow.map(gameData => {
            return (
              <GameCard
                key={`${gameData.awayTeam}${gameData.dateEst}`}
                gameData={gameData}
              />
            )
          })
        )}
      </div>
    </div>
  )
}

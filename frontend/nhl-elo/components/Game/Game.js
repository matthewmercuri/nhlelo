import styles from './Game.module.css'

export default function Game({ gameData }) {
  const homeElo = Math.round(gameData.Home_ELO)
  const awayElo = Math.round(gameData.Away_ELO)

  const homeEloColour = homeElo >= 1500 ? styles.good : styles.bad
  const awayEloColour = awayElo >= 1500 ? styles.good : styles.bad

  return (
    <div className={styles.game}>
      <div className={styles.game__team}>
        <h2>Away Team</h2>
        <h1>{gameData.Away}</h1>
        <p className={awayEloColour}>{awayElo}</p>
      </div>
      <div className={styles.game__team}>
        <h2>Home Team</h2>
        <h1>{gameData.Home}</h1>
        <p className={homeEloColour}>{homeElo}</p>
      </div>
    </div>
  )
}

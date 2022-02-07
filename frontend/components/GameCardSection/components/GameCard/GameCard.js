import styles from './GameCard.module.css'

export default function GameCard({ gameData }) {
  const awayElo = Math.round(gameData.gameEloAway)
  const goodAwayElo = awayElo > 1500
  const homeElo = Math.round(gameData.gameEloHome)
  const goodHomeElo = homeElo > 1500
  console.log(gameData)
  return (
    <div className={styles.gameCard}>
      <div className={styles.left}>
        <div className={styles.homeAwayTag}>AWAY</div>
        <div className={styles.teamInfo}>
          <p className={styles.teamHeader}>{gameData.awayTeam}</p>
          <p className={`${styles.teamElo} ${goodAwayElo ? styles.teamEloGood : styles.teamEloBad}`}>
            {awayElo}
          </p>
        </div>
        <div className={`${styles.matchBox} ${styles.matchBoxLeftRounded}`}>
          <p className={styles.winPercentage}>{`${Math.round(gameData.awayWinProb * 100)}%`}</p>
          <p className={styles.decimalOdds}>{gameData.awayDecimalOdds.toFixed(2)}</p>
        </div>
      </div>
      <div className={styles.left}>
        <div className={`${styles.matchBox} ${styles.matchBoxRightRounded}`}>
          <p className={styles.winPercentage}>{`${Math.round(gameData.homeWinProb * 100)}%`}</p>
          <p className={styles.decimalOdds}>{gameData.homeDecimalOdds.toFixed(2)}</p>
        </div>
        <div className={styles.teamInfo}>
          <p className={styles.teamHeader}>{gameData.homeTeam}</p>
          <p className={`${styles.teamElo} ${goodHomeElo ? styles.teamEloGood : styles.teamEloBad}`}>
            {homeElo}
          </p>
        </div>
        <div className={styles.homeAwayTag}>HOME</div>
      </div>
    </div>
  )
}

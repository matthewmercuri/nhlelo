import styles from "./GameCardSection.module.css"

export default function GameCardSection() {
  return (
    <div className={styles.gameCardSection}>
      <h1>{"today's games"}</h1>
      <div className="accentDiv" />
    </div>
  )
}

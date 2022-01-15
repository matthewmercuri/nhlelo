import EloTable from "./components/EloTable"
import styles from "./EloTableSection.module.css"

export default function EloTableSection() {
  return (
    <div className={styles.EloTableSection}>
      <h1>elo rankings</h1>
      <div className="accentDiv" />
      <div className={styles.EloTableContainer}>
        <EloTable />
      </div>
    </div>
  )
}

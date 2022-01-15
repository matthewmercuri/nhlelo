import Image from "next/image"
import styles from "./LoadingSpinner.module.css"

export default function LoadingSpinner() {
  return (
    <div className={styles.LoadingSpinnerContainer}>
      <Image src={"/images/loading-spinner.svg"} alt="loading spinner" />
    </div>
  )
}

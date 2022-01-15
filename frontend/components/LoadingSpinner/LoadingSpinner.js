import styles from "./LoadingSpinner.module.css"

export default function LoadingSpinner({ size }) {
  let height;
  let width;
  if (size == "large") {
    height = 150
    width = 150
  } else if (size == "medium") {
    height = 100
    width = 100
  } else {
    height = 50
    width = 50
  }

  return (
    <div className={styles.loadingSpinner}>
      <img src={"/images/loading-spinner.svg"} alt="loading spinner" height={height} width={width} />
    </div>
  )
}

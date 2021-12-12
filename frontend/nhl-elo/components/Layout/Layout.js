import NavBar from "../NavBar"
import styles from "./Layout.module.css"

export default function Layout({ children }) {
  return (
    <>
      <NavBar />
      <main className={styles.container}>{children}</main>
    </>
  )
}
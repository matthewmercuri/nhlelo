import Image from "next/image"
import styles from './NavBar.module.css'

export default function NavBar() {
  return (
    <div className={styles.NavBar}>
      <Image src="/images/logo.svg" alt="hockey elo site logo" layout="fill" />
    </div>
  )
}

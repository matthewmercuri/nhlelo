import Link from 'next/link'
import styles from './NavBar.module.css'

export default function NavBar() {
  return (
    <div className={styles.NavBar}>
      <ul>
        <li><Link href='/'>Home</Link></li>
        <li><Link href='/rankings'>Rankings</Link></li>
      </ul>
    </div>
  )
}

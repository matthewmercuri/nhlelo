import { useRef, useState } from "react"
const axios = require("axios").default
import { BASE_URL } from "../../../../services/webapi"
import styles from './EloTable.module.css'

export default function EloTable() {
  const [isLoading, setIsLoading] = useState(true)
  const [hasErrors, setHasErrors] = useState(false)
  const [tableData, setTableData] = useState(null)

  axios.get(`${BASE_URL}/teamelotable`).then(({ data }) => {
    setIsLoading(false)
    setTableData(data.data)
  }).catch(error => {
    setIsLoading(false)
    setHasErrors(true)
  })

  return (
    <div className={styles.EloTable} />
  )
}

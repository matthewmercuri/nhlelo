import NavBar from "../components/NavBar"
import EloTableSection from "../components/EloTableSection"

export default function Home() {
  return (
    <div className={"container"}>
      <section className="mainContent">
        <NavBar />
        <EloTableSection />
      </section>
    </div>
  )
}

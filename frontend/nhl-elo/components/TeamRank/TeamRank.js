export default function TeamRank({ teamData }) {
  const teamName = Object.keys(teamData)[0]
  const teamElo = Math.round(teamData[teamName])
  return (
    <>
      <div>{teamName}</div>
      <div>{teamElo}</div>
    </>
  )
}

export function getWeeklyDateRange(): {
  startDate: string
  endDate: string
} {
  const today = new Date()

  const formatDate = (date: Date): string => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, "0")
    const day = String(date.getDate()).padStart(2, "0")

    return `${year}-${month}-${day}`
  }

  const endDate = new Date(today)
  endDate.setDate(today.getDate() + 6)

  return {
    startDate: formatDate(today),
    endDate: formatDate(endDate),
  }
}

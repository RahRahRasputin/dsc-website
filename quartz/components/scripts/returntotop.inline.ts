document.addEventListener("nav", () => {
  const returnToTopButton = document.getElementById("return-to-top")

  if (!returnToTopButton) return

  const handleScroll = () => {
    // Show button when scrolled down more than 300px
    if (window.scrollY > 300) {
      returnToTopButton.classList.add("visible")
    } else {
      returnToTopButton.classList.remove("visible")
    }
  }

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  }

  returnToTopButton.addEventListener("click", scrollToTop)
  window.addEventListener("scroll", handleScroll)

  // Cleanup
  window.addCleanup(() => {
    returnToTopButton.removeEventListener("click", scrollToTop)
    window.removeEventListener("scroll", handleScroll)
  })

  // Initial check
  handleScroll()
})

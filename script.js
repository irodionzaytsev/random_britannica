async function redirectToRandomLink() {
  try {
    const response = await fetch("articles_array.json");
    if (!response.ok) {
        throw new Error("Failed to load JSON");
    }
    const links = await response.json();
    if (!Array.isArray(links) || links.length === 0) {
      throw new Error("JSON does not contain a non-empty array");
    }
    const randomIndex = Math.floor(Math.random() * links.length);

    window.location.href = links[randomIndex];
  } catch (error) {
    console.error(error);
  }
}

redirectToRandomLink();
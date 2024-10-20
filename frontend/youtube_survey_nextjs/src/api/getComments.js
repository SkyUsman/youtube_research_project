// export default async function getComments(req, res) {
//   try {
//     const response = await fetch("/api/getComments"); // URL of your Flask API that returns random comments
//     const comments = await response.json();

//     if (response.ok) {
//       res.status(200).json(comments);
//     } else {
//       res.status(response.status).json({ message: "Failed to fetch comments" });
//     }
//   } catch (error) {
//     res.status(500).json({ message: "Server error" });
//   }
// }

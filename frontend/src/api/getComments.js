// export default async function getComments(res) {
//   try {
//     const response = await fetch("http://127.0.0.1:5000/api/getComments"); // URL of your Flask API that returns random comments
//     const comments = await response.json();

//     if (res.ok) {
//       response.status(200).json(comments);
//     } else {
//       res.status(response.status).json({ message: "Failed to fetch comments" });
//     }
//   } catch (error) {
//     res.status(500).json({ message: "Server error" });
//   }
// }

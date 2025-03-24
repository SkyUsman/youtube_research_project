// export default async function postResponses(req, res) {
//   if (req.method === "POST") {
//     try {
//       const response = await fetch("http://127.0.0.1:5000/api/postResponses", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(req.body),
//       });

//       if (response.ok) {
//         res.status(200).json({ message: "Success" });
//       } else {
//         res
//           .status(response.status)
//           .json({ message: "Failed to submit responses" });
//       }
//     } catch (error) {
//       res.status(500).json({ message: "Server error" });
//     }
//   } else {
//     res.setHeader("Allow", ["POST"]);
//     res.status(405).end(`Method ${req.method} Not Allowed`);
//   }
// }

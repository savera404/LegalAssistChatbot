

const LawyerTable = ({ lawyers }) => {

  const handleLawyerClick = (lawyerId) => {
    window.parent.postMessage(
      { type: "NAVIGATE_TO_LAWYER", id: lawyerId },
      "http://localhost:3000"  // replace * with your main project's origin in production e.g. "https://yourmainproject.com"
    );
  };

  return (
    <div>
      <p>Here are some lawyers you can consult:</p>
      <table>
        <thead>
          <tr>
            <th>Lawyer</th>
            <th>Practice Area</th>
            <th>City</th>
            <th>Experience</th>
          </tr>
        </thead>
        <tbody>
          {lawyers.map((lawyer) => (
            <tr key={lawyer.id}>
              <td>
                <span
                  onClick={() => handleLawyerClick(lawyer.id)}
                  style={{
                    cursor: "pointer",
                    fontWeight: "bold",
                    textDecoration: "underline",
                    color: "inherit"
                  }}
                >
                  {lawyer.name}
                </span>

              </td>
              <td>{lawyer.practiceArea}</td>
              <td>{lawyer.city}</td>
              <td>{lawyer.experience} years</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LawyerTable;
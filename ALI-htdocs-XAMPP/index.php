<!DOCTYPE html>
<html>
<head>
	<title>Attendance Records</title>
	<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
	<style>
	  /* High-tech theme with black and gray color scheme */
	  /* High-tech box styles */
	  .high-tech-box {
	    border-radius: 20px;
	    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
	    padding: 20px;
	    background-color: #292929;
	  }
	  
	  /* Titre styles */
	  .title {
	    font-family: 'Open Sans', sans-serif;
	    font-size: 28px;
	    color: #fff;
	    text-align: center;
	    padding: 10px;
	    background-color: #000;
	    border-radius: 20px 20px 0px 0px;
	  }

	  /* Table styles */
	  table {
	    border-collapse: collapse;
	    width: 100%;
	  }

	  th, td {
	    padding: 12px;
	    text-align: left;
	    border-bottom: 1px solid #ddd;
	    color: #fff;
	  }

	  th {
	    background-color: #212121;
	  }

	  tr:nth-child(even) {
	    background-color: #212121;
	  }

	  tr:hover {
	    background-color: #292929;
	  }

	  /* Mode sombre */
	  body {
	    background-color: #000;
	    color: #fff;
	  }

	  /* Animation styles */
	  @keyframes fadeInUp {
	    from {
	      opacity: 0;
	      transform: translateY(20px);
	    }
	    to {
	      opacity: 1;
	      transform: translateY(0px);
	    }
	  }

	  .fadeInUp {
	    animation-name: fadeInUp;
	    animation-duration: 0.5s;
	  }

	  iframe {
	    width: 73%;
	    height: 500px;
	    border: none;
	    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	    border-radius: 10px;
	  }
	</style>
</head>
<script>
    setInterval(function(){
        location.reload();
    }, 2000);
</script>

<body>
	<div class="container">
		<h1>Attendance Records</h1>
		<table class="table table-striped table-bordered">
			<thead class="table-header">
				<tr>
					<th id="name-column">Name</th>
					<th id="time-column">Time</th>
					<th id="card-column">Card</th>
					<th id="qrcode-column">QR Code</th>
					<th id="authentication-column">Auth</th>
				</tr>
			</thead>
			<tbody>
				<?php
					// Database connection settings
					$host = "localhost";
					$username = "root";
					$password = "";
					$dbname = "test";

					// Create connection
					$conn = new mysqli($host, $username, $password, $dbname);

					// Check connection
					if ($conn->connect_error) {
						die("Connection failed: " . $conn->connect_error);
					}

					// SQL query to retrieve all data from the attendance table
					$sql = "SELECT * FROM attendance";
					$result = $conn->query($sql);

					// Check if there are any results
					if ($result->num_rows > 0) {
						// Loop through each row of data
						while($row = $result->fetch_assoc()) {
    						echo "<tr class='table-row'>";
   							echo "<td>" . $row['name'] . "</td>";
    						echo "<td>" . $row['time'] . "</td>";
    						echo "<td>" . $row['card'] . "</td>";
    						echo "<td>" . $row['qrcode'] . "</td>";
    
    						// Set the background color of the "Auth" column based on the authentication value
    						if ($row['authentication'] == 'TRUE') {
        					echo "<td style='background-color: green'>" . $row['authentication'] . "</td>";
   							 } else {
        					echo "<td style='background-color: red'>" . $row['authentication'] . "</td>";
    						}
    
   							 echo "</tr>";
}

					} else {
						echo "<tr><td colspan='5'>No attendance records found.</td></tr>";
					}


					// Close database connection
					$conn->close();
	?>
</div>
				</table>
				</body>
				<h2>ESP-32 CAM </h2>
				<iframe style="border: 5px solid white;" width="1000" height="1000" src="http://192.168.43.158/cam-hi.jpg" frameborder="0" scrolling="no" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

				</html>
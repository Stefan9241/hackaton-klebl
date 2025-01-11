import React, { useState } from "react";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import { Box, Button, Snackbar, Alert, Typography } from "@mui/material";

const DrawingsPage: React.FC = () => {
  // Sample data
  const rows = [
    { id: 1, pdfName: "ProjectPlan.pdf", dateAdded: "2023-12-01" },
    { id: 2, pdfName: "DesignSpecs.pdf", dateAdded: "2023-12-05" },
    { id: 3, pdfName: "Blueprint.pdf", dateAdded: "2023-12-10" },
  ];

  // Snackbar state
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [downloadedFile, setDownloadedFile] = useState<string | null>(null);

  // Handle snackbar close
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
    setDownloadedFile(null);
  };

  // Handle download button click
  const handleDownload = (fileName: string) => {
    // Trigger the download (mock action)
    console.log(`Downloading ${fileName}`);
    setDownloadedFile(fileName);
    setSnackbarOpen(true);
  };

  // Column definitions
  const columns: GridColDef[] = [
    { field: "pdfName", headerName: "PDF Name", flex: 1 },
    { field: "dateAdded", headerName: "Date Added", flex: 1 },
    {
      field: "download",
      headerName: "Download",
      flex: 0.5,
      sortable: false,
      renderCell: (params) => (
        <Button
          variant="contained"
          color="primary"
          size="small"
          onClick={() => handleDownload(params.row.pdfName)}
        >
          Download
        </Button>
      ),
    },
  ];

  return (
    <Box sx={{ height: 400, width: "100%", padding: 2 }}>
      {/* Typography Header */}
      <Typography variant="h4" gutterBottom color="primary">
        Drawings
      </Typography>

      <DataGrid rows={rows} columns={columns} />

      {/* Snackbar */}
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={handleSnackbarClose}
          severity="success"
          sx={{ width: "100%" }}
        >
          {downloadedFile
            ? `${downloadedFile} downloaded successfully!`
            : "Downloaded successfully!"}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default DrawingsPage;

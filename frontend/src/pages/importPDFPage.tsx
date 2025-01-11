import React, { useState } from "react";
import { Document, Page } from "react-pdf";
import { Button, Snackbar, Typography } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import { Box } from "@mui/system";
import { pdfjs } from "react-pdf";
import { Allotment } from "allotment";
import axios from "axios";
import "react-pdf/dist/esm/Page/TextLayer.css";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "allotment/dist/style.css";
import Editor from "@monaco-editor/react";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

const ImportPdfPage: React.FC = () => {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
  const [jsonData, setJsonData] = useState<string>("");

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file) {
      setPdfFile(file);

      try {
        const response = await axios.get(
          "https://jsonplaceholder.typicode.com/posts/1"
        );
        setJsonData(JSON.stringify(response.data, null, 2));
      } catch (error) {
        console.error("Error fetching data", error);
        setJsonData(JSON.stringify({ error: "Failed to fetch data" }, null, 2));
      }
    }
  };

  const handleSubmit = async () => {
    try {
      const parsedJson = JSON.parse(jsonData);
      console.log("Form Data:", parsedJson);
      // const response = await axios.post("your-api-endpoint", parsedJson);
      // console.log("Submitted JSON:", response.data);
      setJsonData("");
      setSnackbarOpen(true);
      setPdfFile(null);
      setPageNumber(1);
      setSnackbarOpen(true);
    } catch (error) {
      console.error("Error submitting JSON:", error);
    }
  };

  const handleSnackbarClose = (
    event?: React.SyntheticEvent | Event,
    reason?: string
  ) => {
    if (reason === "clickaway") {
      return;
    }
    setSnackbarOpen(false);
  };

  const handleEditorChange = (value: string | undefined) => {
    if (value) {
      setJsonData(value);
    }
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <Typography variant="h4" gutterBottom sx={{ padding: 2 }} color="primary">
        Import PDF Drawing
      </Typography>

      <Allotment>
        {/* Left Pane: JSON Editor Section */}
        <Box sx={{ padding: 2, height: "100%" }}>
          <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>
            <input
              type="file"
              onChange={handleFileChange}
              accept="application/pdf"
            />
            {jsonData && (
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
              >
                Submit
              </Button>
            )}
          </Box>
          <Box sx={{ marginTop: 3, height: "calc(100% - 60px)" }}>
            <Editor
              height="100%"
              defaultLanguage="json"
              value={jsonData}
              onChange={handleEditorChange}
              options={{
                readOnly: false,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                theme: "vs-white",
              }}
            />
          </Box>
        </Box>

        {/* Right Pane: PDF Preview */}
        <Box
          sx={{
            padding: 2,
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          {pdfFile ? (
            <>
              <Typography variant="h6" sx={{ marginBottom: 2 }}>
                PDF Preview
              </Typography>
              <Box
                sx={{
                  flex: 1,
                  overflowY: "auto",
                  overflowX: "auto",
                  "&::-webkit-scrollbar": {
                    width: "8px",
                  },
                  "&::-webkit-scrollbar-thumb": {
                    backgroundColor: "#888",
                    borderRadius: "4px",
                  },
                }}
              >
                <Document
                  file={pdfFile}
                  loading={<Typography>Loading PDF...</Typography>}
                >
                  <Page
                    pageNumber={pageNumber}
                    renderTextLayer={false}
                    loading={<Typography>Loading page...</Typography>}
                  />
                </Document>
              </Box>
            </>
          ) : (
            <Typography>No PDF selected</Typography>
          )}
        </Box>
      </Allotment>

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <MuiAlert
          onClose={handleSnackbarClose}
          severity="success"
          sx={{
            width: "100%",
            padding: 2,
            fontSize: "1.2rem",
            maxWidth: "500px",
          }}
        >
          Submitted successfully!
        </MuiAlert>
      </Snackbar>
    </Box>
  );
};

export default ImportPdfPage;
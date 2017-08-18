$(function() {
    var __PDF_DOC,
	__PAGE_RENDERING_IN_PROGRESS = 0,
	__CANVAS = $('#pdf-canvas').get(0),
	__CANVAS_CTX = __CANVAS.getContext('2d');

    function showPDF(pdf_url) {
	$("#pdf-loader").show();

	PDFJS.getDocument({ url: pdf_url }).then(function(pdf_doc) {
	    __PDF_DOC = pdf_doc;
	    
	    // Hide the pdf loader and show pdf container in HTML
	    $("#pdf-loader").hide();
	    $("#pdf-contents").show();

	    // Show the first page
	    showPage(1);
	}).catch(function(error) {
	    // If error re-show the upload button
	    $("#pdf-loader").hide();
	    $("#upload-button").show();
	    
	    alert(error.message);
	});;
    }

    function showPage(page_no) {
	__PAGE_RENDERING_IN_PROGRESS = 1;

	// While page is being rendered hide the canvas and show a loading message
	$("#pdf-canvas").hide();
	$("#page-loader").show();

	// Fetch the page
	__PDF_DOC.getPage(page_no).then(function(page) {
	    // As the canvas is of a fixed width we need to set the scale of the viewport accordingly
	    var scale_required = __CANVAS.width / page.getViewport(1).width;

	    // Get viewport of the page at required scale
	    var viewport = page.getViewport(scale_required);

	    // Set canvas height
	    __CANVAS.height = viewport.height;

	    var renderContext = {
		canvasContext: __CANVAS_CTX,
		viewport: viewport
	    };
	    
	    // Render the page contents in the canvas
	    page.render(renderContext).then(function() {
		__PAGE_RENDERING_IN_PROGRESS = 0;

		// Show the canvas and hide the page loader
		$("#pdf-canvas").show();
		$("#page-loader").hide();
	    });
	});
    }

    // When user chooses a PDF file
    $("#uploaded_file").on('change', function() {
	// Validate whether PDF
	if(['application/pdf'].indexOf($("#uploaded_file").get(0).files[0].type) == -1) {
	    alert('Error: Not a PDF');
	    return;
	}

	// Send the object url of the pdf
	showPDF(URL.createObjectURL($("#uploaded_file").get(0).files[0]));
    });
});

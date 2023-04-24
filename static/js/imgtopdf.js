const convertBtn = document.getElementById('convert-btn');
const inputFile = document.getElementById('input-files');

convertBtn.addEventListener('click', () => {
  const files = inputFile.files;
  const fileUrls = [];

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const fileUrl = URL.createObjectURL(file);
    fileUrls.push(fileUrl);
  }

  const pdfDoc = new jsPDF();

  const addImagesToPdf = (imageUrls, index) => {
    const imageUrl = imageUrls[index];
    const img = new Image();
    img.src = imageUrl;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0, img.width, img.height);
      const imageData = canvas.toDataURL('image/jpeg');
      pdfDoc.addImage(imageData, 'JPEG', 0, 0, img.width, img.height);
      if (index < imageUrls.length - 1) {
        addImagesToPdf(imageUrls, index + 1);
      } else {
        pdfDoc.save('converted.pdf');
      }
    };
  };

  addImagesToPdf(fileUrls, 0);
});

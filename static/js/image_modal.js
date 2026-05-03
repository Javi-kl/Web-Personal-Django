function openImageModal(imageUrl, altText) {
  const modal = document.getElementById('image-modal');
  const modalImage = document.getElementById('modal-image');
  modalImage.src = imageUrl;
  modalImage.alt = altText;
  modal.showModal();
}
function closeImageModal() {
  document.getElementById('image-modal').close();
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeImageModal();
  }
});
document.getElementById('image-modal').addEventListener('click', (e) => {
  if (e.target.tagName !== 'IMG') {
    closeImageModal();
  }
});
document.querySelectorAll(".project-image-trigger").forEach((el) => {
  el.addEventListener("click", function () {
    openImageModal(this.dataset.modalUrl, this.dataset.modalAlt);
  });
});
document.querySelector('.image-modal-close').addEventListener('click', closeImageModal);
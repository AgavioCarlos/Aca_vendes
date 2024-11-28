const carouselContainer = document.querySelector('.carousel-container');
  const images = document.querySelectorAll('.carousel-image');
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');
  
  let currentIndex = 0;

  function showImage(index) {
    const imageWidth = images[0].clientWidth;
    carouselContainer.style.transform = `translateX(${-index * imageWidth}px)`;
  }

  nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(currentIndex);
  });

  prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
  });

  // Inicializa con la primera imagen
  showImage(currentIndex);

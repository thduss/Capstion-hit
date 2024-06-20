import React from 'react';

const StarRating = ({ rating, maxRating = 10 }) => {
  const totalStars = 5;
  // const adjustedRating = (rating / maxRating) * totalStars; => 아고다
  const adjustedRating = 5;
  const filledStars = Math.floor(adjustedRating);
  const halfStar = adjustedRating % 1 !== 0;
  const emptyStars = totalStars - filledStars - (halfStar ? 1 : 0);

  return (
    <div className="star bg-#FFF0CE rounded-xl">
      {[...Array(filledStars)].map((_, index) => (
        <svg
          key={`filled-${index}`}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          className="w-6 h-6 filled"
        >
          <path d="M12 .587l3.668 7.431L24 9.748l-6 5.851 1.417 8.274L12 18.896l-7.417 3.977L6 15.599 0 9.748l8.332-1.73L12 .587z" fill="#ffd700"/>
        </svg>
      ))}
      {halfStar && (
        <svg
          key="half"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          className="w-6 h-6 half-filled"
        >
          <defs>
            <linearGradient id="halfGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="50%" stopColor="#ffd700" />
              <stop offset="50%" stopColor="#D9D9D9" stopOpacity="1" />
            </linearGradient>
          </defs>
          <path d="M12 .587l3.668 7.431L24 9.748l-6 5.851 1.417 8.274L12 18.896l-7.417 3.977L6 15.599 0 9.748l8.332-1.73L12 .587z" fill="url(#halfGradient)" />
        </svg>
      )}
      {[...Array(emptyStars)].map((_, index) => (
        <svg
          key={`empty-${index}`}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          className="w-6 h-6 unfilled"
        >
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
        </svg>
      ))}
    </div>
  );
};

export default StarRating;

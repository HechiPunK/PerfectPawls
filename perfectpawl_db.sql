-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-12-2024 a las 20:00:03
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `perfectpawl_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `adoptions`
--

CREATE TABLE `adoptions` (
  `id_adoption` int(11) NOT NULL,
  `image` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` enum('Dog','Cat','Other','') NOT NULL,
  `sex` enum('Male','Female') NOT NULL,
  `age` enum('Puppy','Adult','Senior') NOT NULL,
  `size` enum('Small','Medium','Large') NOT NULL,
  `color` enum('Black','White','Brown','Golden','Cream','Gray','Brindle','Merle','Blue','Orange','Tabby','Tortoiseshell','Spotted/Dappled') NOT NULL,
  `sterilized` enum('Yes','No') NOT NULL,
  `vaccinated` enum('Yes','No') NOT NULL,
  `description` text NOT NULL,
  `id_sesion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `adoptions`
--

INSERT INTO `adoptions` (`id_adoption`, `image`, `name`, `type`, `sex`, `age`, `size`, `color`, `sterilized`, `vaccinated`, `description`, `id_sesion`) VALUES
(1, 'img/Bruno2.png', 'Bruno', 'Dog', 'Male', 'Puppy', 'Small', 'Cream', 'Yes', 'Yes', 'He is very small and friendly', 1),
(3, 'img/Luci.png', 'Luci', 'Cat', 'Male', 'Adult', 'Medium', 'Black', 'Yes', 'Yes', 'Calm, mysterious, and loves to nap.', 1),
(4, 'img/Julian.png', 'Julian', 'Dog', 'Male', 'Adult', 'Small', 'Brown', 'Yes', 'No', 'Always happy, energetic, and loves attention.', 2),
(5, 'img/Golden.png', 'Maximiliano', 'Dog', 'Male', 'Senior', 'Large', 'Golden', 'Yes', 'Yes', 'He is very loyal.', 2),
(6, 'img/Sam.png', 'Sam', 'Dog', 'Female', 'Adult', 'Large', 'Brown', 'Yes', 'Yes', 'Very energetic.', 2),
(7, 'img/Garfield.png', 'Garfield', 'Cat', 'Male', 'Adult', 'Medium', 'Orange', 'No', 'Yes', 'Eats a lot and hates mondays.', 3),
(8, 'img/Ciclope.png', 'Misho', 'Cat', 'Male', 'Puppy', 'Small', 'White', 'No', 'No', 'Curious, soft, and likes to explore.', 3),
(9, 'img/perro_negro.png', 'Firulais', 'Dog', 'Male', 'Adult', 'Large', 'Black', 'Yes', 'Yes', 'Very loyal and protective.', 3),
(10, 'img/gatosss.png', 'Maxi', 'Cat', 'Male', 'Adult', 'Medium', 'Orange', 'Yes', 'Yes', 'Very lovelly', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `shelters`
--

CREATE TABLE `shelters` (
  `id_shelter` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` char(250) NOT NULL,
  `email` varchar(100) NOT NULL,
  `address` varchar(250) NOT NULL,
  `manager` varchar(250) NOT NULL,
  `description` text NOT NULL,
  `img` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `shelters`
--

INSERT INTO `shelters` (`id_shelter`, `name`, `password`, `email`, `address`, `manager`, `description`, `img`) VALUES
(1, 'Refugio1', 'scrypt:32768:8:1$bQXhnh8zVVkGzaLo$ce1d9997314e03fae532d8897718dd6c8ab896ead4f8915ef9a79c86482702f7a12078c82b780366a1273704eead44d09957f3e2d350e9aa50be56070c412812', 'mrzelda332@gmail.com', 'plaza sesamo', 'refugio', 'un refugio que mas esperas papu :V', '0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `socioeconomic`
--

CREATE TABLE `socioeconomic` (
  `id_socioeconomic` int(11) NOT NULL,
  `pregunta1` enum('$600 - $900 MXN','$900 - $1100 MXN','$1100 - $1400 MXN','More than $1400 MXN') NOT NULL,
  `pregunta2` enum('Limited space (only a small apartment or studio)','Moderate space (apartment with a terrace or small yard)','Ample space (house with a large garden or play area)','') NOT NULL,
  `pregunta3` enum('Only once a day','Twice a day','Three times a day or more','None') NOT NULL,
  `pregunta4` enum('Less than 1 hour','Between 1 and 2 hours','More than 2 hours','None') NOT NULL,
  `pregunta5` enum('"Yes, and they are agree','Yes, they are not agree','No, i live alone','') NOT NULL,
  `pregunta6` text NOT NULL,
  `id_sesion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `socioeconomic`
--

INSERT INTO `socioeconomic` (`id_socioeconomic`, `pregunta1`, `pregunta2`, `pregunta3`, `pregunta4`, `pregunta5`, `pregunta6`, `id_sesion`) VALUES
(1, '$1100 - $1400 MXN', 'Moderate space (apartment with a terrace or small yard)', 'Three times a day or more', 'Between 1 and 2 hours', '', 'I like cats', 6),
(2, '$1100 - $1400 MXN', 'Moderate space (apartment with a terrace or small yard)', 'Three times a day or more', 'More than 2 hours', '', 'i love cats', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id_sesion` int(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `mail` varchar(50) NOT NULL,
  `password` char(200) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `profile_pic` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `address` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id_sesion`, `username`, `mail`, `password`, `phone`, `profile_pic`, `description`, `address`) VALUES
(1, 'Sebas777', 'sebastia6251@gmail.com', 'scrypt:32768:8:1$eZmJNKsQ1zyZUkaI$b052db45c0727a5d4b387909a57ffa4c0336caaf64b5f7fe307ccd4d19409ff343361a6356768c4fd8a24bbd6822be83c8320f7a0543005a74d46587940fc13d', '6143219645', '', '', ''),
(2, 'Mrzelda', 'mrzelda332@gmail.com', 'scrypt:32768:8:1$51a0a9xe1hn68fQp$500c49c18240ce2ea79779f443563d4b60e3ba9ba1dadc4b76d26ffb0a280e8dddad9c7af95c97a8388344f946c5ffea0223544aec329ed89eef5cd3eb463cb4', '6145339879', '', '', ''),
(3, 'Andu66', 'andreadloya@gmail.com', 'scrypt:32768:8:1$KEyNkjTxLocO7wPY$565b4b5fc45e6b894a2fd4cda840d0901c299bd228cb54d56842c4feb4ebf4fe631c7579f6d9bb4ca9e5f95defd08b328df7f872c5d53481980ee838acceca17', '6141549639', '', '', ''),
(4, 'KiangChong', 'klcgkiang098@gmail.com', 'scrypt:32768:8:1$HlrmpM5hERjNvZcp$b0f2075f6fc8465588b5d1a1c785bb8b47de04e096e2bfa1d98a573874e66bd5316f7e08c48c6caca9ad13882397c79cadae7b00607c9905f1c06e5c6a3b61a6', '6144569974', '', '', ''),
(5, 'Sebas55', 'sebastia_5@outlook.com', 'scrypt:32768:8:1$9zeXu3osoI4NeOhM$36f0bedd9905fbb6d0852252979f9dd88195419b4e6c56e1a90ab35d9885d90cc142ae4ab599d95a75d6993bb56ab9eead20608579f29eacf62f51d79c9333d0', '6143219645', 'profile_pics/gatosss.png', 'I love cats', 'Laguna de la vieja'),
(6, 'KiangChong55', 'kian@hotmail.com', 'scrypt:32768:8:1$SFnmtG29V37oZe0x$093806e4a50ce84460213dcc7a6a143830bc5f9237a488bd367df0a0dcca1f623e9549297957c854ea305ee5400d9eba1be743f8a38f5b270227c16680fa01e2', '6141234566', 'profile_pics/profile.png', 'i love cats', 'Laguna de la vieja'),
(7, 'Perfectpawl', 'perfectpawl@gmail.com', 'scrypt:32768:8:1$2L76jqw5JumgVq6G$4566889d45445e02409f051476d7b4a9cca49951aa37dc2cbb0161441778f232dbf11c18a0c601efa110400e2cd5420a6992c54ae9314a4d9bbea31d783c7fc8', '6141234566', 'profile_pics/profile.png', 'i love cats', 'Laguna de la vieja');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `adoptions`
--
ALTER TABLE `adoptions`
  ADD PRIMARY KEY (`id_adoption`);

--
-- Indices de la tabla `shelters`
--
ALTER TABLE `shelters`
  ADD PRIMARY KEY (`id_shelter`);

--
-- Indices de la tabla `socioeconomic`
--
ALTER TABLE `socioeconomic`
  ADD PRIMARY KEY (`id_socioeconomic`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_sesion`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `adoptions`
--
ALTER TABLE `adoptions`
  MODIFY `id_adoption` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `shelters`
--
ALTER TABLE `shelters`
  MODIFY `id_shelter` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `socioeconomic`
--
ALTER TABLE `socioeconomic`
  MODIFY `id_socioeconomic` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id_sesion` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

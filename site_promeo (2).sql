-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 12 juin 2024 à 12:28
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `site_promeo`
--

-- --------------------------------------------------------

--
-- Structure de la table `centres`
--

CREATE TABLE `centres` (
  `id` int(11) NOT NULL,
  `Ville` varchar(255) DEFAULT NULL,
  `Adresse` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `formations`
--

CREATE TABLE `formations` (
  `id` int(11) NOT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  `id_centre` int(11) DEFAULT NULL,
  `id_formateur` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `rdvs`
--

CREATE TABLE `rdvs` (
  `id` int(11) NOT NULL,
  `Heure` time DEFAULT NULL,
  `Duree` time DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `id_formateur` int(11) DEFAULT NULL,
  `id_formation` int(11) DEFAULT NULL,
  `Nom` varchar(255) DEFAULT NULL,
  `Prenom` varchar(255) DEFAULT NULL,
  `Mail` varchar(255) DEFAULT NULL,
  `Telephone` varchar(255) DEFAULT NULL,
  `Url_invitation` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Déchargement des données de la table `rdvs`
--

INSERT INTO `rdvs` (`id`, `Heure`, `Duree`, `Date`, `id_formateur`, `id_formation`, `Nom`, `Prenom`, `Mail`, `Telephone`, `Url_invitation`) VALUES
(2, '15:20:00', '00:20:00', '2024-05-28', NULL, NULL, 'meri', 'wesley', 'wesley60290@gmail.com', '0684840316', ''),
(3, '15:20:00', '00:20:00', '2024-05-29', NULL, NULL, 'meri', 'wesley', 'wesley60290@gmail.com', '0684840316', ''),
(4, '15:00:00', '03:00:00', '2024-05-28', NULL, NULL, 'meri', 'wesley', 'wesley60290@gmail.com', '0684840316', ''),
(5, '14:55:00', '00:20:00', '2024-06-11', NULL, NULL, 'meri', 'wesley', 'wesley60290@gmail.com', '0684840316', '');

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nom` varchar(50) DEFAULT NULL,
  `prenom` varchar(50) DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `MDP` varchar(50) DEFAULT NULL,
  `etudiant_promeo` tinyint(1) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`id`, `nom`, `prenom`, `date_naissance`, `mail`, `MDP`, `etudiant_promeo`, `role`) VALUES
(1, 'admin', 'admin', NULL, 'admin@promeo.fr', 'Admin123', 1, 'admin'),
(6, 'DECUY', 'René-Michel', '2003-04-20', 'RMD@promeo.fr', 'RMD_200403', 0, 'etudiant'),
(7, 'AAAA', 'AAAA', NULL, 'AAAA@promeo.fr', 'azerty', NULL, 'formateur');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `centres`
--
ALTER TABLE `centres`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `formations`
--
ALTER TABLE `formations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_centre` (`id_centre`),
  ADD KEY `id_formateur` (`id_formateur`);

--
-- Index pour la table `rdvs`
--
ALTER TABLE `rdvs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_formateur` (`id_formateur`),
  ADD KEY `id_formation` (`id_formation`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `centres`
--
ALTER TABLE `centres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `formations`
--
ALTER TABLE `formations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `rdvs`
--
ALTER TABLE `rdvs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

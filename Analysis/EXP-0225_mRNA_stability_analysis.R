# EXP-0225 mRNA Stability Analysis Script
# Analysis of YBX1 knockdown effect on mRNA half-life in Huh7 and HepG2 cells
# Authors: james-m-jordan, jack-zhao
# Date: 2025-05-12

# Load required libraries
library(tidyverse)
library(rtracklayer)
library(ggplot2)
library(cowplot)
library(DESeq2)

# Set paths
experiment_id <- "EXP-0225"
data_dir <- file.path("Data", experiment_id, "raw")
output_dir <- file.path("Data", experiment_id, "figures")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Load qPCR data
# Assuming format: sample, gene, timepoint, Ct, cell_line, treatment
qpcr_data <- read_excel(file.path(data_dir, "timecourse_qPCR.xlsx"))

# Load RNA concentration data
rna_data <- read_excel(file.path(data_dir, "RNA_concentrations.xlsx"))

# Define reference genes
ref_genes <- c("GAPDH", "ACTB")
target_genes <- c("IL6", "MYC")

# Calculate delta Ct (normalize to reference genes)
calculate_delta_ct <- function(df) {
  # First calculate average Ct of reference genes per sample
  ref_data <- df %>% 
    filter(gene %in% ref_genes) %>%
    group_by(sample, timepoint, cell_line, treatment) %>%
    summarize(ref_ct = mean(Ct), .groups = "drop")
  
  # Calculate delta Ct for all genes
  df %>%
    left_join(ref_data, by = c("sample", "timepoint", "cell_line", "treatment")) %>%
    mutate(delta_ct = Ct - ref_ct)
}

# Calculate delta-delta Ct (relative to t=0)
calculate_relative_expression <- function(df) {
  # First get delta Ct values
  delta_ct_df <- calculate_delta_ct(df)
  
  # For each gene, cell line, and treatment, get the t=0 value
  t0_values <- delta_ct_df %>%
    filter(timepoint == "0h") %>%
    select(gene, cell_line, treatment, delta_ct) %>%
    rename(delta_ct_0 = delta_ct)
  
  # Calculate delta-delta Ct and relative expression (2^-ddCt)
  delta_ct_df %>%
    left_join(t0_values, by = c("gene", "cell_line", "treatment")) %>%
    mutate(
      delta_delta_ct = delta_ct - delta_ct_0,
      rel_expr = 2^(-delta_delta_ct),
      ln_rel_expr = log(rel_expr)
    )
}

# Function to calculate mRNA half-life
calculate_half_life <- function(expr_data) {
  # Convert timepoint to numeric hours
  expr_data <- expr_data %>%
    mutate(
      hours = case_when(
        timepoint == "0h" ~ 0,
        timepoint == "1h" ~ 1,
        timepoint == "2h" ~ 2,
        timepoint == "4h" ~ 4,
        timepoint == "8h" ~ 8,
        TRUE ~ NA_real_
      )
    )
  
  # Calculate half-life for each gene, cell line, and treatment
  expr_data %>%
    filter(!is.na(hours)) %>%
    group_by(gene, cell_line, treatment) %>%
    do({
      # Fit linear model: ln(expression) ~ time
      model <- lm(ln_rel_expr ~ hours, data = .)
      # Extract slope (k)
      k <- coef(model)[2]
      # Calculate half-life: t1/2 = ln(2)/|k|
      t_half <- log(2)/abs(k)
      
      # Return results
      tibble(
        slope = k,
        half_life = t_half,
        r_squared = summary(model)$r.squared,
        p_value = summary(model)$coefficients[2,4]
      )
    })
}

# PLACEHOLDER: Data processing steps (to be filled with actual data)
# 1. Read and process data
# normalized_data <- calculate_relative_expression(qpcr_data)

# 2. Calculate half-lives
# half_lives <- calculate_half_life(normalized_data)

# 3. Compare half-lives: control vs YBX1 knockdown
# half_life_comparison <- half_lives %>%
#   select(gene, cell_line, treatment, half_life) %>%
#   pivot_wider(
#     names_from = treatment,
#     values_from = half_life,
#     names_prefix = "t_half_"
#   ) %>%
#   mutate(
#     ratio = t_half_siYBX1 / t_half_siCTRL,
#     percent_change = (ratio - 1) * 100
#   )

# PLACEHOLDER: Plot generation (to be filled with actual data)
# Plot example: mRNA decay curves for each gene in Huh7 cells
plot_decay_curves <- function(data, cell_line_to_plot) {
  # Filter for the specific cell line and target genes
  plot_data <- data %>%
    filter(cell_line == cell_line_to_plot, gene %in% target_genes)
  
  # Create decay plot
  ggplot(plot_data, aes(x = hours, y = ln_rel_expr, color = treatment, shape = treatment)) +
    geom_point(size = 3) +
    geom_smooth(method = "lm", se = TRUE, alpha = 0.2) +
    facet_wrap(~gene, scales = "free_y") +
    labs(
      title = paste("mRNA Decay Curves in", cell_line_to_plot, "Cells"),
      x = "Time after Actinomycin D (hours)",
      y = "ln(Relative Expression)",
      color = "Treatment",
      shape = "Treatment"
    ) +
    scale_color_manual(values = c("siCTRL" = "blue", "siYBX1" = "red")) +
    theme_cowplot() +
    theme(legend.position = "bottom")
}

# PLACEHOLDER: Save results
# Example code for saving results
save_results <- function(half_life_df) {
  # Save summary table
  write_csv(half_life_df, file.path(output_dir, "half_life_summary.csv"))
  
  # Create comparison table for manuscript
  comparison_table <- half_life_df %>%
    select(gene, cell_line, treatment, half_life) %>%
    pivot_wider(
      names_from = c(cell_line, treatment),
      values_from = half_life
    )
  
  write_csv(comparison_table, file.path(output_dir, "half_life_comparison_table.csv"))
}

# PLACEHOLDER: Main execution (commented out until real data is available)
# Process and analyze data
# normalized_data <- calculate_relative_expression(qpcr_data)
# half_lives <- calculate_half_life(normalized_data)

# Generate and save plots
# huh7_decay_plot <- plot_decay_curves(normalized_data, "Huh7")
# ggsave(file.path(output_dir, "Huh7_decay_curves.pdf"), huh7_decay_plot, width = 10, height = 8)
# 
# hepg2_decay_plot <- plot_decay_curves(normalized_data, "HepG2")
# ggsave(file.path(output_dir, "HepG2_decay_curves.pdf"), hepg2_decay_plot, width = 10, height = 8)

# Save numerical results
# save_results(half_lives)

# Final output
cat("
========================================
EXP-0225 mRNA Stability Analysis Results
========================================

# To be updated with actual results after data collection

Analysis completed: 2025-05-12
Results saved to:", output_dir, "\n") 
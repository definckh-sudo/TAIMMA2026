"""EQ10–EQ12: suy giảm chất lượng, cold storage, ngưỡng nhận hàng."""

def lambda_effective(lam, lambda_mult, cold, rho_cold):
    """EQ11: λ_eff = λ·M_λ·(1 − ρ_cold·1[cold])."""
    return lam * lambda_mult * (1 - rho_cold * (1 if cold else 0))

def survival(lam_eff, T):
    """EQ10: s_T = (1 − λ_eff)^T."""
    return (1 - lam_eff) ** T

def accepted(s_T, s_min):
    """EQ12 / D8: lô được nhận nếu s_T ≥ s_min."""
    return s_T >= s_min

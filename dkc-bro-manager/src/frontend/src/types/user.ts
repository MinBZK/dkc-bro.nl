export type User = {
  email: string;
  admin: boolean;
  id: number;
  org_name: string;
  org_code: string;
  org_id: number;
};

export type UserCreated = {
  email: string;
  admin: boolean;
  totp_seed: string;
  totp_seed_qr: string;
};

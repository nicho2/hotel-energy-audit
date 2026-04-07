export type ProjectListItem = {
  id: string;
  name: string;
  client_name: string | null;
  status: string;
  wizard_step: number | string;
};

import { Request, Response } from 'express';

export const LogGPTResponse = (req: Request, res: Response) => {
  // Example logic to get a user
  res.send('Get User');
};

export const createUser = (req: Request, res: Response) => {
  // Example logic to create a user
  res.send('Create User');
};
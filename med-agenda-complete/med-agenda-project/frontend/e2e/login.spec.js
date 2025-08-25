import { test, expect } from '@playwright/test';

test('login and open calendar', async ({ page }) => {
  await page.goto('/');
  // fill login form
  await page.fill('input[placeholder="Correo"]', 'admin@medagenda.com');
  await page.fill('input[placeholder="Contraseña"]', 'adminpass');
  await page.click('button:has-text("Ingresar")');
  // wait for calendar to appear
  await page.waitForSelector('.fc-daygrid-day');
  expect(await page.title()).toContain('MedAgenda');
});

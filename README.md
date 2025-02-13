# Discord Bot Verification System README

## 🇬🇧 English Version
### Overview
This Discord bot enables moderators to bulk-verify users, remove their verification roles, send confirmation messages, and log actions.

### Breakdown of `*potvrdit` Command:
```python
@bot.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def potvrdit(ctx, *user_ids):
    role = ctx.guild.get_role(VERIFIED_ROLE_ID)
    log_channel = ctx.guild.get_channel(LOG_CHANNEL_ID)
    for user_id in user_ids:
        member = ctx.guild.get_member(int(user_id))
        if member:
            await member.remove_roles(role)
            await member.send('🎉 Verification confirmed by a moderator!')
            await log_channel.send(f'✅ {member.display_name} verified by {ctx.author.display_name}')
```
- **Command Trigger:** `*potvrdit <user_id1> <user_id2>`
- **Role Removal:** `await member.remove_roles(role)`
- **DM User:** `await member.send()`
- **Log Event:** `await log_channel.send()`

### Editable Sections:
1. **Bot Prefix:** Change `command_prefix='*'`.
2. **Role Management:** Modify `remove_roles` or use `add_roles`.
3. **DM Text:** Customize `member.send()`.
4. **Log Format:** Edit `log_channel.send()`.

### Required Permissions:
- Manage Roles, View Channels, Send Messages, Read Message History
- Enable `message_content` intent

---
## 🇨🇿 Česká Verze
### Přehled
Tento Discord bot umožňuje moderátorům hromadně ověřovat uživatele, odstraňovat ověřovací role, posílat soukromé zprávy a logovat akce.

### Rozbor Příkazu `*potvrdit`:
```python
@bot.command()
@commands.has_role(MODERATOR_ROLE_ID)
async def potvrdit(ctx, *user_ids):
    role = ctx.guild.get_role(VERIFIED_ROLE_ID)
    log_channel = ctx.guild.get_channel(LOG_CHANNEL_ID)
    for user_id in user_ids:
        member = ctx.guild.get_member(int(user_id))
        if member:
            await member.remove_roles(role)
            await member.send('🎉 Ověření potvrzeno moderátorem!')
            await log_channel.send(f'✅ {member.display_name} ověřen uživatelem {ctx.author.display_name}')
```
- **Spuštění:** `*potvrdit <user_id1> <user_id2>`
- **Odebrání role:** `await member.remove_roles(role)`
- **Zpráva:** `await member.send()`
- **Logování:** `await log_channel.send()`

### Části Kódu K Editaci:
1. **Prefix:** `command_prefix='*'`
2. **Správa Rolí:** Změnit na `add_roles()` nebo `remove_roles()`.
3. **Obsah DM:** Úprava textu v `member.send()`.
4. **Formát Logů:** Změna zprávy v `log_channel.send()`.

### Potřebná Oprávnění:
- Spravovat role, Číst kanály, Odesílat zprávy, Číst historii zpráv
- Aktivace `message_content` intent

